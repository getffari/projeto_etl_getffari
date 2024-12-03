create schema if not exists minio.bruto with (location = 's3a://bruto/');
        
create table if not exists 
	minio.bruto.musicas (
		musica VARCHAR,
		artista VARCHAR,
		gravadora VARCHAR
	) 
with (
	    external_location = 's3a://bruto/musicas',
	    format = 'CSV',
	    skip_header_line_count=1,
		csv_separator = ';'
    )
;

create table if not exists 
	minio.bruto.trackData (
		trackDataId VARCHAR,
		name VARCHAR,
		album VARCHAR,
		artistsData VARCHAR,
		release_date VARCHAR
	) 
with (
	    external_location = 's3a://bruto/trackData',
	    format = 'CSV',
	    skip_header_line_count=1,
		csv_separator = ';'
    )
;

create table if not exists 
	minio.bruto.artistsData (
		name VARCHAR,
		genres VARCHAR,
		popularity VARCHAR,
		followers VARCHAR
	) 
with (
	    external_location = 's3a://bruto/artistsData',
	    format = 'CSV',
	    skip_header_line_count=1,
		csv_separator = ';'
    )
;

create schema if not exists minio.refinado with (location = 's3a://refinado/');

create table if not exists 
	minio.refinado.artistByTrackId (
		trackId VARCHAR,
		artist VARCHAR
	) 
with (
	    external_location = 's3a://refinado/artistByTrackId',
	    format = 'CSV',
	    skip_header_line_count=1,
		csv_separator = ';'
    )
;

create table if not exists 
	minio.refinado.artistsData (
		name VARCHAR,
		popularity VARCHAR,
		followers VARCHAR
	) 
with (
	    external_location = 's3a://refinado/artistsData',
	    format = 'CSV',
	    skip_header_line_count=1,
		csv_separator = ';'
    )
;

create table if not exists 
	minio.refinado.genresByArtist (
		artistName VARCHAR,
		genre VARCHAR
	) 
with (
	    external_location = 's3a://refinado/genresByArtist',
	    format = 'CSV',
	    skip_header_line_count=1,
		csv_separator = ';'
    )
;

create table if not exists 
	minio.refinado.musicas (
		trackDataId VARCHAR,
		musica VARCHAR,
		artista VARCHAR,
		gravadora VARCHAR
	) 
with (
	    external_location = 's3a://refinado/musicas',
	    format = 'CSV',
	    skip_header_line_count=1,
		csv_separator = ';'
    )
;

create table if not exists 
	minio.refinado.trackData (
		trackId VARCHAR,
		name VARCHAR,
		album VARCHAR,
		release_date VARCHAR
	) 
with (
	    external_location = 's3a://refinado/trackData',
	    format = 'CSV',
	    skip_header_line_count=1,
		csv_separator = ';'
    )
;
    