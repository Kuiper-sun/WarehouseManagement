FROM php:8.2-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    libpq-dev

# Install PHP extensions
RUN docker-php-ext-install pdo_pgsql mbstring exif pcntl bcmath gd

# Get latest Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www/html

# Copy existing application directory contents
COPY . .

# <<< --- ADD THE FOLLOWING LINES --- >>>
# Set ownership for storage and cache directories to the web server user.
# The user 'www-data' is the default user for both Nginx and PHP-FPM.
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

# Set write permissions for the group and others on these directories.
RUN chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache
# <<< --- END OF ADDED LINES --- >>>

# Expose port 9000 and start php-fpm server
EXPOSE 9000
CMD ["php-fpm"]