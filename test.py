#!/usr/bin/env python
import pyppp

if __name__ == '__main__':
    print 'PyPPP Version: %s' % pyppp.__version__
    p = pyppp.PyPPP()
    print 'PPP Specification Version: %s' % p.__version__
    p.generate_random_sequence_key()
    print 'PPP Key: %s' % p.key
    passcode = 5
    print 'Passcode: %d' % passcode
    print '%s' % p.retrieve_passcode(passcode)
