from django.urls import path
from app import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index),
    path('home', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('delete-account', views.delete_account, name='delete-account'),
    
    path('manage', views.manage, name='manage'),
    
    # Products
    path('products', views.products, name='products'),
    path('add-product', views.add_product),
    path('add-product-image', views.add_product_image),
    
    # Fields
    path('add-field', csrf_exempt(views.add_field)),
    path('get-fields', views.get_fields),
    path('delete-field', views.delete_field),
    
    # Property
    path('add-property', views.add_property),
    path('delete-property', views.delete_property),
    
    # Input Type
    path('add-input-type', views.add_input_type),
    
    # Components Index
    path('components', views.components, name='components'),    
    
    # Components
    path('components-alerts', views.components_alerts, name='components-alerts'),
    path('components-accordion', views.components_accordion, name='components-accordion'),
    path('components-badges', views.components_badges, name='components-badges'),
    path('components-breadcrumbs', views.components_breadcrumbs, name='components-breadcrumbs'),
    path('components-buttons', views.components_buttons, name='components-buttons'),
    path('components-cards', views.components_cards, name='components-cards'),
    path('components-carousel', views.components_carousel, name='components-carousel'),
    path('components-list-group', views.components_list_group, name='components-list-group'),
    path('components-modal', views.components_modal, name='components-modal'),
    path('components-tabs', views.components_tabs, name='components-tabs'),
    path('components-pagination', views.components_pagination, name='components-pagination'),
    path('components-progress', views.components_progress, name='components-progress'),
    path('components-spinners', views.components_spinners, name='components-spinners'),
    path('components-tooltips', views.components_tooltips, name='components-tooltips'),
    path('forms-elements', views.forms_elements, name='forms-elements'),
    path('forms-layouts', views.forms_layouts, name='forms-layouts'),
    path('forms-editors', views.forms_editors, name='forms-editors'),
    path('forms-validation', views.forms_validation, name='forms-validation'),
    path('tables-general', views.tables_general, name='tables-general'),
    path('tables-data', views.tables_data, name='tables-data'),
    path('charts-chartjs', views.charts_chartjs, name='charts-chartjs'),
    path('charts-apexcharts', views.charts_apexcharts, name='charts-apexcharts'),
    path('charts-echarts', views.charts_echarts, name='charts-echarts'),
    path('icons-bootstrap', views.icons_bootstrap, name='icons-bootstrap'),
    path('icons-remix', views.icons_remix, name='icons-remix'),
    path('icons-boxicons', views.icons_boxicons, name='icons-boxicons'),
    path('users-profile', views.users_profile, name='users-profile'),
    path('pages-faq', views.pages_faq, name='pages-faq'),
    path('pages-contact', views.pages_contact, name='pages-contact'),
    path('pages-error-404', views.pages_error_404, name='pages-error-404'),
    path('pages-blank', views.pages_blank, name='pages-blank'),
]