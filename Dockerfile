# Use the official Nginx image as the base image
FROM nginx:alpine

# Copy the frontend files to the Nginx html directory
COPY frontend /usr/share/nginx/html

# Copy the Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 