<?php
/** Theme setup and WooCommerce support for Wattks Shop. */
if (!defined('ABSPATH')) exit;

function wattks_shop_setup() {
    load_theme_textdomain('wattks-shop', get_template_directory() . '/languages');
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('woocommerce');
    add_theme_support('custom-logo');
    register_nav_menus(['primary' => __('منوی اصلی', 'wattks-shop')]);
}
add_action('after_setup_theme', 'wattks_shop_setup');

function wattks_shop_assets() {
    wp_enqueue_style('wattks-shop', get_stylesheet_uri(), [], '1.0.0');
}
add_action('wp_enqueue_scripts', 'wattks_shop_assets');
