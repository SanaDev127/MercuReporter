from .views import *
from django.urls import path

urlpatterns = [
    path("transaction_upload/<int:id>/", upload_transaction_file, name='transaction_upload'),
    path("view_upload_effects/<int:id>/", preview_transaction_effects, name="preview_upload"),
    path("save_upload/<int:id>/", save_transaction_file_upload, name='save_upload'),
    path("transaction_list/<int:id>/", transaction_list, name='transaction_list'),
    path("receipt_scan/", scan_transaction_receipt, name='scan_receipt'),



]
