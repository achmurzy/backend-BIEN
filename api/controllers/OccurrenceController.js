/**
 * OccurrenceController
 *
 * @description :: Server-side logic for managing occurrences
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */
module.exports = {
  list: function (req, res) {
  	sails.log(req);
  	var store = Occurrence.getDatastore();
    store.sendNativeQuery('SELECT * FROM view_full_occurrence_individual_dev LIMIT 1000', function(err, results) {
      if (err) {
        res.status(400);
      } else {
        res.send(results);
      }
    });
  }
};
