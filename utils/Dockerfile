FROM alpine:3.20

WORKDIR /app

RUN apk add --no-cache curl

COPY traffic-generator.sh traffic-generator.sh

RUN chmod +x traffic-generator.sh

ENTRYPOINT [ "./traffic-generator.sh" ]
