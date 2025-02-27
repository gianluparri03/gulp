class GULPError(Exception):
    pass

ErrEmailNotAvailable = GULPError('Email not available')
ErrUnknown = GULPError('Unknown error')
ErrWrongCredentials = GULPError('Wrong email or password')
ErrUserUnkwnown = GULPError('Unknown user')
ErrWrongToken = GULPError('Something went wrong')
