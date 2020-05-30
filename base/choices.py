
# Choice for ROLE_FB
ROLE_FB = 1
# Choice for ROLE_TWITTER
ROLE_TWITTER = 2

# Choice for Provider
PROVIDER = (
    (ROLE_FB, 'fb'),
    (ROLE_TWITTER, 'twitter')
)

# Choice for SINGLE
SINGLE = 1
# Choice for RANGE
RANGE = 2

# Choice for PRIZE_RANGE_TYPE
PRIZE_RANGE_TYPE = (
    (SINGLE, 'single'),
    (RANGE, 'range')
)

# Choice for MEMBERSHIP
MEMBERSHIP = 1

# Choice for PRODUCT_SERVICE
PRODUCT_SERVICE = 2

# Choice for PRIZE_TYPE
PRIZE_TYPE = (
    (MEMBERSHIP, 'membership'),
    (PRODUCT_SERVICE, 'product_service'),
)
