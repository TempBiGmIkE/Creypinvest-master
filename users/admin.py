from django.contrib import admin

from users.models import Profile, Wallet, Transaction, AdminWallet, AdminTransaction, KycDocument

admin.site.register(AdminWallet)
admin.site.register(AdminTransaction)
admin.site.register(Profile)
admin.site.register(Wallet)
admin.site.register(Transaction)
@admin.register(KycDocument)
class KycDocumentAdmin(admin.ModelAdmin):
	list_display = ("profile", "document_type", "status", "uploaded_at")
	list_filter = ("document_type", "status")
	search_fields = ("profile__user__username", "profile__user__email")
	actions = ["approve_documents", "reject_documents"]

	def approve_documents(self, request, queryset):
		for obj in queryset:
			obj.approve()
		self.message_user(request, f"Approved {queryset.count()} documents")

	approve_documents.short_description = "Approve selected KYC documents"

	def reject_documents(self, request, queryset):
		for obj in queryset:
			obj.reject()
		self.message_user(request, f"Rejected {queryset.count()} documents")

	reject_documents.short_description = "Reject selected KYC documents"
