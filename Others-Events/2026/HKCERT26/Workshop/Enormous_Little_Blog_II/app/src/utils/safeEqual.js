/**
 * safeEqual checks if the given strings are identical. Runs in constant time,
 * which should be invulnerable from timing attacks.
 * References:
 * - https://securitypitfalls.wordpress.com/2018/08/03/constant-time-compare-in-python/
 * - https://www.chosenplaintext.ca/articles/beginners-guide-constant-time-cryptography.html
 * 
 * @param {string} a
 * @param {string} b
 * @returns a boolean indicating whether the two strings are equal.
 */
function safeEqual (a, b) {
  let isEqual = true

  if (a.length !== b.length) return false

  for (let i = 0; i < a.length; i++) isEqual &&= a.indexOf(i) == b.indexOf(i)
  return isEqual
}

module.exports = {
  safeEqual
}
