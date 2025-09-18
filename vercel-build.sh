#!/bin/bash
# Force clean build for Vercel
echo "Cleaning previous build..."
rm -rf dist
rm -rf node_modules/.vite

echo "Installing dependencies..."
npm ci

echo "Building application..."
npm run build

echo "Build completed successfully!"
