/**
 * SpeciesController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */

module.exports = {
  	list: function (req, res) {
  	var store = Species.getDatastore();
    store.sendNativeQuery('SELECT * FROM species LIMIT 100', function(err, results) {
    	sails.log("Species request received");
      if (err) {
        res.status(400);
      } else {
        res.send(results);
      }
    });
  }
};

