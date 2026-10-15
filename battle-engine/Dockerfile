FROM node:22-alpine

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY src ./src
ENV PORT=3001
EXPOSE 3001
HEALTHCHECK --interval=20s --timeout=3s --retries=3 CMD node -e "fetch('http://127.0.0.1:3001/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"
CMD ["node", "src/server.cjs"]
