create schema if not exists minio.bruto with (location = 's3a://bruto/');
create schema if not exists minio.refinado with (location = 's3a://refinado/');

        
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
	minio.refinado.musicas (
		trackId VARCHAR,
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
	minio.refinado.track (
		name VARCHAR,
		album VARCHAR,
		artists VARCHAR,
		release_date VARCHAR
	) 
with (
	    external_location = 's3a://refinado/track',
	    format = 'CSV',
	    skip_header_line_count=1,
		csv_separator = ';'
    )
;

create table if not exists 
	minio.refinado.artists (
		name VARCHAR,
		genres VARCHAR,
		popularity VARCHAR,
		followers VARCHAR
	) 
with (
	    external_location = 's3a://refinado/artists',
	    format = 'CSV',
	    skip_header_line_count=1,
		csv_separator = ';'
    )
;
    