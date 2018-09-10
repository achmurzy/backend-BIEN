/**
 * Occurrence.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  schema: true,
  tableName: 'view_full_occurrence_individual_dev',
  primaryKey: 'taxonobservation_id',
  attributes: {
  	taxonobservation_id: {type: 'number', required: true},
  	longitude: {type: 'number'},
  	latitude: {type: 'number'},
  	scrubbed_species_binomial: {type: 'string'}
  }
};

