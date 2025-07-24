FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install system build dependencies required for native modules (e.g. pdf-parse)
# We install them with a virtual label so they can be removed afterwards to keep the
# final image small.  libc6-compat is added for some pre-built binaries that
# expect glibc.
RUN apk add --no-cache --virtual .build-deps \
        python3 make g++ \
    && apk add --no-cache libc6-compat \
    && npm install --production \
    && apk del .build-deps

# Create uploads directory
RUN mkdir -p uploads

# Copy source code
COPY . .

# Expose port
EXPOSE 3003

# Start the application
CMD ["node", "server.js"] 