FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Create uploads directory
RUN mkdir -p uploads

# Copy source code
COPY . .

# Expose port
EXPOSE 3003

# Start the application
CMD ["node", "server.js"] 