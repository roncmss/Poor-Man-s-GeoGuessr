
import google_streetview.api


params = [{
	'size': '800x800',
	'location': '1.2882178, 103.8591591',
	'fov': '90',
	'heading': '0',
	'key': 'AIzaSyDq5PxpIawewkm5I1AlDkNcmai05bWGkqg',
	'source': 'outdoor'
}]


results = google_streetview.api.results(params)


results.download_links('downloads')
print(results.metadata)