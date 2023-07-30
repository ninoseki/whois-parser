# ref. https://github.com/cheenanet/whois-servers-list/blob/master/limit-reached-messages.json
WHOIS_RATE_LIMIT_MESSAGES: set[str] = {
    "WHOIS LIMIT EXCEEDED - SEE WWW.PIR.ORG/WHOIS FOR DETAILS",
    "Your access is too fast,please try again later.",
    "Your connection limit exceeded.",
    "Number of allowed queries exceeded.",
    "WHOIS LIMIT EXCEEDED",
    "Requests of this client are not permitted.",
    "Too many connection attempts. Please try again in a few seconds.",
    "We are unable to process your request at this time.",
    "HTTP/1.1 400 Bad Request",
    "Closing connections because of Timeout",
    "Access to whois service at whois.isoc.org.il was **DENIED**",
    "IP Address Has Reached Rate Limit",
}
