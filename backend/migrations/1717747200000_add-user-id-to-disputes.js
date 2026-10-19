/* eslint-disable camelcase */

exports.up = (pgm) => {
  pgm.addColumns('disputes', {
    user_id: { type: 'text' },
  });
  pgm.createIndex('disputes', 'user_id');
};

exports.down = (pgm) => {
  pgm.dropIndex('disputes', 'user_id');
  pgm.dropColumns('disputes', ['user_id']);
};
