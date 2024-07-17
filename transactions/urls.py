from .views import *
from django.urls import path

urlpatterns = [
    path("transaction_upload/<int:id>/", upload_transaction_file, name='transaction_upload'),
    path("view_upload_effects", preview_transaction_effects, name="preview_upload"),
    path("save_upload/", save_transaction_file_upload, name='save_upload'),
    path("receipt_scan/", scan_transaction_receipt, name='scan_receipt'),


]
