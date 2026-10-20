/* eslint-disable camelcase */

exports.shorthands = undefined;

exports.up = (pgm) => {
  // Add CHECK constraint to markets.status column
  // Valid statuses: 'open', 'locked', 'resolved', 'cancelled'
  pgm.addConstraint('markets', 'markets_status_check', {
    check: "status IN ('open', 'locked', 'resolved', 'cancelled')",
  });
};

exports.down = (pgm) => {
  // Remove the CHECK constraint
  pgm.dropConstraint('markets', 'markets_status_check');
};
