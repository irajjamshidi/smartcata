<?php get_header(); ?>
<main class="container section"><div class="section-heading"><div><h1><?php bloginfo('name'); ?></h1><p><?php bloginfo('description'); ?></p></div></div><?php if (have_posts()) : while (have_posts()) : the_post(); the_content(); endwhile; endif; ?></main>
<?php get_footer(); ?>
