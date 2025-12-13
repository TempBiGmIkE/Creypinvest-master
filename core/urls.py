from django.urls import path
from core.views import (
    about,
    contact,
    send_contact_email,
    # Investment plans
    investment_plans_browse_view,
    investment_plan_detail_view,
    subscribe_to_plan_view,
    investment_dashboard_view,
    subscription_detail_view,
    add_contribution_view,
    pause_subscription_view,
    resume_subscription_view,
)

urlpatterns = [
    path("about-us/", about, name="about-us"),
    path("contact-us/", contact, name="contact-us"),
    path("send-mail/contact-us/", send_contact_email, name="send_contact_email"),
    
    # Investment Plans URLs
    path("investment-plans/", investment_plans_browse_view, name="investment_plans_browse"),
    path("investment-plans/<int:plan_id>/", investment_plan_detail_view, name="plan_detail"),
    path("investment-plans/<int:plan_id>/subscribe/", subscribe_to_plan_view, name="subscribe_plan"),
    path("investment/dashboard/", investment_dashboard_view, name="investment_dashboard"),
    path("investment/subscription/<int:subscription_id>/", subscription_detail_view, name="subscription_detail"),
    path("investment/subscription/<int:subscription_id>/contribute/", add_contribution_view, name="add_contribution"),
    path("investment/subscription/<int:subscription_id>/pause/", pause_subscription_view, name="pause_subscription"),
    path("investment/subscription/<int:subscription_id>/resume/", resume_subscription_view, name="resume_subscription"),
]
