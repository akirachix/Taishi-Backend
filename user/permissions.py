from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class IsAuthenticatedAndHasPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm("view_cases")


class HasJudgePermissions(BasePermission):
    """
    Custom permission for judges.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "judge":
            judge_permissions = [
                "view_cases",
                "edit_cases",
                "view_hearings",
                "schedule_hearings",
                "view_case_details",
            ]
            return all(request.user.has_perm(perm) for perm in judge_permissions)
        return False


class HasAdminPermissions(BasePermission):
    """
    Custom permission for admin users with full access.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "admin":
            admin_permissions = [
                "view_dashboard",
                "view_product_metrics",
                "view_model_metrics",
                "manage_users",
                "view_active_users",
                "view_signups",
                "view_processing_time",
                "edit_system_settings",
                "view_detailed_analytics",
            ]
            return all(request.user.has_perm(perm) for perm in admin_permissions)
        return False


class ReadOnlyAccess(BasePermission):
    """
    Custom permission to allow read-only access for authenticated users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in SAFE_METHODS
