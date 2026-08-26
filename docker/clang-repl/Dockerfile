FROM alpine:3.24

RUN apk add --no-cache \
    clang22-extra-tools \
    rlwrap \
    coreutils

ENTRYPOINT ["rlwrap", "-H", "/tmp/.clang-repl-history", \
            "stdbuf", "-o0", "clang-repl"]
