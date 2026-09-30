<!doctype html>
<html <?php language_attributes(); ?> dir="rtl">
<head><meta charset="<?php bloginfo('charset'); ?>"><meta name="viewport" content="width=device-width, initial-scale=1"><?php wp_head(); ?></head>
<body <?php body_class(); ?>><?php wp_body_open(); ?>
<div class="notice"><div class="container"><span>ارسال رایگان برای سفارش‌های بالای ۲ میلیون تومان</span><a href="#support">پشتیبانی و مشاوره تخصصی ←</a></div></div>
<header class="site-header"><div class="container nav"><a class="brand" href="<?php echo esc_url(home_url('/')); ?>"><span class="brand-mark">ϟ</span>WATTKS</a><nav class="primary-nav" aria-label="منوی اصلی"><?php wp_nav_menu(['theme_location'=>'primary','container'=>false,'fallback_cb'=>'wattks_shop_default_menu','items_wrap'=>'%3$s']); ?></nav><div class="actions"><button class="icon-button" aria-label="جست‌وجو">⌕</button><a class="icon-button" href="<?php echo esc_url(function_exists('wc_get_cart_url') ? wc_get_cart_url() : '#'); ?>" aria-label="سبد خرید">🛒</a><span class="cart-count"><?php echo function_exists('WC') && WC()->cart ? esc_html(WC()->cart->get_cart_contents_count()) : '۰'; ?></span></div></div></header>
<?php function wattks_shop_default_menu(){ echo '<a href="#categories">دسته‌بندی‌ها</a><a href="#products">پرفروش‌ترین‌ها</a><a href="#offer">پیشنهاد ویژه</a><a href="#support">راهنمای خرید</a>'; } ?>
