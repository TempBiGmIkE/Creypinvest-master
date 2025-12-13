from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from creyp.utils import random_string_generator, file_cleanup, image_resize

from PIL import Image
from django_countries.fields import CountryField


STATUS = (
    ("pending", "pending"),
    ("hidden", "hidden"),
    ("credit", "credit"),
    ("processing", "processing"),
    ("confirming", "confirming"),
    ("error", "error"),
    ("failed", "failed")
)
GENDER = (
    ("female", "female"),
    ("male", "male"),
    ("other", "other")
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to="profile-image/%h/%Y/",
                              default="profile-image-placeholder.png")
    gender = models.CharField(max_length=15, choices=GENDER, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    country = CountryField(blank=True)
    signup_confirmation = models.BooleanField(default=False)
    deposit_before = models.BooleanField(default=False)
    referred_by = models.ForeignKey("Profile", on_delete=models.CASCADE, blank=True, null=True)
    refer_clicks = models.IntegerField(default=0, blank=True, null=True)
    refers = models.ManyToManyField(User, related_name="refers", blank=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    # verification level: 0 = none, 1 = basic KYC, 2 = financials, 3 = full (loan agreements + documents)
    verification_level = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
    @property
    def first_name(self):
        return self.user.first_name
    
    @property
    def last_name(self):
        return self.user.last_name

    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)
            if self.image.storage.exists(self.image.name):
                image_resize(self.image, 512, 512)
        else:
            super().save(*args, **kwargs)

    def update_verification_level(self):
        """Compute verification level based on approved KYC documents."""
        # Import here to avoid circular import at module import time
        try:
            docs = self.kycdocument_set.filter(status='approved')
            types = set(d.document_type for d in docs)
            level = 0
            if 'id' in types:
                level = 1
            if 'financial' in types:
                level = max(level, 2)
            if 'loan' in types:
                level = max(level, 3)
            self.verification_level = level
            self.save()
        except Exception:
            pass


class Wallet(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    btc_address = models.TextField(blank=True, null=True)
    balance = models.CharField(max_length=100, default="00.00", blank=True)
    pin = models.CharField(max_length=6, blank=True)
    amount_invested = models.CharField(max_length=100, default="00.00", blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.btc_address} - bal : {self.balance}"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=15, choices=STATUS)
    msg = models.TextField(blank=True)
    transactionId = models.CharField(max_length=17, blank=True)
    hash_id = models.CharField(max_length=17, blank=True, null=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-timestamp', '-id']

    def __str__(self):
        return f"user has {self.wallet.balance} | TID: {self.transactionId}"

    def save(self, *args, **kwargs):
        self.hash_id = random_string_generator(size=17)
        super().save(*args, **kwargs)


class AdminWallet(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    btc_address = models.TextField(unique=True)
    returns = models.CharField(max_length=100, blank=True)
    bad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.btc_address}"

class AdminTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100, blank=True)
    amount = models.CharField(max_length=100, blank=True)
    btc_address = models.TextField()
    msg = models.TextField(blank=True)
    transactionId = models.CharField(max_length=17, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.plan == "withdraw":
            return f"{self.wallet.btc_address} debited ${self.amount}"
        else:
            return f"{self.wallet.btc_address} transfered ${self.amount}"


DOCUMENT_TYPES = (
    ("id", "Identity Document"),
    ("financial", "Financial Records"),
    ("loan", "Loan Agreement"),
    ("other", "Other"),
)

DOC_STATUS = (
    ("pending", "pending"),
    ("approved", "approved"),
    ("rejected", "rejected"),
)


class KycDocument(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to="kyc/%Y/%m/%d/")
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=DOC_STATUS, default="pending")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.profile.user.username} - {self.document_type} ({self.status})"

    def approve(self):
        self.status = "approved"
        self.save()
        # Update profile verification level when a doc is approved
        try:
            self.profile.update_verification_level()
        except Exception:
            pass

    def reject(self):
        self.status = "rejected"
        self.save()
        try:
            self.profile.update_verification_level()
        except Exception:
            pass

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=Profile)
def update_wallet_signal(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


post_delete.connect(
    file_cleanup, sender=Image, dispatch_uid="profile.image.file_cleanup"
)
