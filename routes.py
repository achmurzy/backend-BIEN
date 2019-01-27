from flask import jsonify, request
import requests

from server import app, session
from models import Species, Occurrence, Taxon, Range

###
#DON'T FORGET @ WHEN YOU DECORATE ROUTES
#app.route("") doesn't throw an error!!!
###

#Returns a limited number of species for testing data queries
@app.route("/species")
def get_species():
	species_response = session.query(Species).limit(1000)
	return jsonify([spp.json for spp in species_response])

#String matching for user queries of species names
@app.route("/species/")
def match_species():
	species = request.args.get('species')
	species = species.replace("_", " ")+"%"
	species_response = session.query(Species).filter(Species.species.like(species)).all()
	return jsonify([spp.json for spp in species_response])

#Returns all occurrences for a given species
@app.route("/occurrences/")
def get_occurrences():
	species = request.args.get('species')
	species = species.replace("_", " ")
	species_response = session.query(Taxon).filter_by(species=species).first();
	species_id = species_response.species_taxon_id
	occurrence_response = session.query(Occurrence).filter_by(species_taxon_id=species_id)
	return jsonify([occ.json for occ in occurrence_response])

@app.route("/ranges/")
def get_ranges():
	species = request.args.get('species')
	range_response = session.query(Range.geom.ST_AsGeoJSON()).filter_by(species=species).first()
	return jsonify(range_response)
	#return jsonify([range.json for range in range_response])