FROM alpine AS thttpd

ARG THTTPD_VERSION=2.29

# Install all dependencies required for compiling thttpd
RUN apk add --no-cache gcc musl-dev make

# Download thttpd sources
RUN wget https://www.acme.com/software/thttpd/thttpd-${THTTPD_VERSION}.tar.gz \
  && tar xzf thttpd-${THTTPD_VERSION}.tar.gz \
  && mv /thttpd-${THTTPD_VERSION} /thttpd

# Compile thttpd to a static binary
RUN cd /thttpd \
  && ./configure \
  && make CCOPT="-O2 -s -static" thttpd

RUN adduser -D static

FROM node:alpine as node

COPY src ./src/
COPY package.json .babelrc ./
RUN npm install --legacy-peer-deps
RUN npm run build

FROM scratch

# Copy over the user
COPY --from=thttpd /etc/passwd /etc/passwd

# Copy the thttpd static binary
COPY --from=thttpd /thttpd/thttpd /

USER static
WORKDIR /home/static

COPY index.html manifest.json app.py mcu.py disassembler.py ./
COPY assets ./assets/
COPY --from=node lib/bundle.min.js ./lib/bundle.min.js
COPY --from=node node_modules/brython/brython.min.js node_modules/brython/brython_stdlib.js ./node_modules/brython/

EXPOSE 3000

CMD ["/thttpd", "-D", "-h", "0.0.0.0", "-p", "3000", "-d", "/home/static", "-u", "static", "-l", "-", "-M", "31536000"]
