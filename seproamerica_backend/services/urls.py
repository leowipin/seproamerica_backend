from django.urls import path
from .views import ServiceView, ServiceNamesView, ServiceGetView, OrderClientView, OrderClientNamesView, OrderAllView, OrderListRestView, OrderPendingView, OrderAcceptedView, OrderPaidView, OrderProcessView, OrderDeletedView, OrderEndedView, OrderRefundView, BillingCreateView, StatusChangeView, PhoneAccountOrderView, OrderReportView, PhoneAccountOrders, LeaderStaff

urlpatterns = [
    path('service/', ServiceView.as_view(), name='service'),
    path('serviceByID/', ServiceGetView.as_view(), name='servicebyid'),
    path('serviceNames/', ServiceNamesView.as_view(), name='servicenames'),
    path('orderClient/', OrderClientView.as_view(), name='orderclient'),
    path('orderClientNames/', OrderClientNamesView.as_view(), name='orderclientnames'),
    path('orderAll/', OrderAllView.as_view(), name='orderall'),
    path('ordersRestList/', OrderListRestView.as_view(), name='ordersrestlist'),
    path('ordersPending/', OrderPendingView.as_view(), name='orderspending'),
    path('ordersAccepted/', OrderAcceptedView.as_view(), name='ordersaccepted'),
    path('ordersPaid/', OrderPaidView.as_view(), name='orderspaid'),
    path('ordersProcess/', OrderProcessView.as_view(), name='ordersprocess'),
    path('ordersDeleted/', OrderDeletedView.as_view(), name='ordersdeleted'),
    path('ordersEnded/', OrderEndedView.as_view(), name='ordersended'),
    path('ordersRefund/', OrderRefundView.as_view(), name='ordersrefund'),
    path('billing/', BillingCreateView.as_view(), name='billingcreate'),
    path('statusChange/', StatusChangeView.as_view(), name='statuschange'),
    path('phoneAccountOrdersList/', PhoneAccountOrders.as_view(), name='phoneaccountorderslist'),
    path('phoneAccountOrder/', PhoneAccountOrderView.as_view(), name='phoneaccountorder'),
    path('orderReport/', OrderReportView.as_view(), name='orderreport'),
    path('leaderStaff/', LeaderStaff.as_view(), name='leaderstaff'),
]