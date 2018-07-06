# Monero seed "encryption" is vulnerable to known-plaintext key recovery

<p align="center"><img src="https://ryo-currency.com/img/svg/ryo-privacy-for-everyone.svg" width="300"></p>

### TLDR section

Adding a random number to your plaintext is not encryption unfortunately… I wish it was that simple. If you are using Monero's seed encryption feature and you are unsure about the implications of this weakness you should generate a new wallet, send all your funds to it and encrypt your seed using gpg's symmetric encryption feature.

### Where is the bug?

https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/cryptonote_format_utils.cpp#L1100

### Why is it a problem?

Adding a random number which represents the password to the paintext compromises any other ciphertext that shares the same password if a plaintext is ever revealed. In cryptographic parlance this is known as a key recovery attack.

### How can it be fixed?

The problem is caused by shoehorning security into an old format - 25 word format does not have enough room to fit an IV. Encrypted seed should be extended by 6 words to include a 64-bit IV and a proper encryption algorithm should be used to protect it. Alternatively a GPG-like message format should replace words.

### Why not report it though Monero’s VRP or HackerOne?

Monero project has a fairly long-standing tradition of attacking security researchers [[ 1 ]](https://www.reddit.com/r/Monero/comments/5q60b3/security_issue_in_cryptonoteuniversalpool/dd24sbz/) [[ 2 ]](https://twitter.com/fireice_uk/status/977167686097690624) [[ 3 ]](https://hackerone.com/reports/291489). I don't consider the money to be worth the aggro. If that position ever changes in the future, I will be happy to work with them.

### Is this bug present in Ryo?

No, we removed the seed encryption feature for now.
