from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from .models import UserProfile
from pymongo import MongoClient
import os

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['phone_number'].required = True
        return formset

# Unregister the default User admin
admin.site.unregister(User)

# Register with custom configuration
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Ensure UserProfile exists
        if not hasattr(obj, 'userprofile'):
            UserProfile.objects.create(user=obj, phone_number="")
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, UserProfile):
                if not instance.phone_number:
                    raise ValidationError("Phone number is required for all users.")
                
                # UPDATE MONGODB WITH PHONE NUMBER
                self.update_mongodb_phone(form.instance.username, instance.phone_number)
                
        super().save_formset(request, form, formset, change)
    
    def update_mongodb_phone(self, username, phone_number):
        """Update phone number in MongoDB when admin saves"""
        try:
            MONGODB_URL = os.getenv("mongo_login_FRONTEND")
            mongo_client = MongoClient(MONGODB_URL)
            db = mongo_client["main"]
            users_collection = db["users"]
            
            # Update the phone number in MongoDB
            users_collection.update_one(
                {"Username": username},
                {"$set": {"Phone_Number": phone_number}}
            )
            mongo_client.close()
        except Exception as e:
            print(f"Error updating MongoDB: {e}")