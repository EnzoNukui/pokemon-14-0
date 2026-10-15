'use strict';

const CHOICE_PATTERN = /^(move [1-4](?: (?:mega|zmove))?|switch [1-6]|team [1-6]{1,6}|pass)$/;

function isSupportedChoice(choice) {
  return typeof choice === 'string' && CHOICE_PATTERN.test(choice);
}

module.exports = { isSupportedChoice };
