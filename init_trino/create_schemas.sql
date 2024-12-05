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

create schema if not exists minio.consulta with (location = 's3a://refinado/');

create or replace view minio.consulta.view_musicas as
	select
		a.name as nome_musica
		,a.album as album_musica
		,a.release_date as data_lancamento
		,b.gravadora
		,c.artist as artista
		,d.popularity as popularidade_artista
		,d.followers as seguidores_artista
		,e.genre as genero_artista
	from
		minio.refinado.trackdata as a
	inner join
		minio.refinado.musicas as b
			on a.trackid = b.trackdataid
	inner join
		minio.refinado.artistbytrackid as c
			on a.trackid = c.trackid
	inner join
		minio.refinado.artistsdata as d
			on c.artist = d.name
	left join
		minio.refinado.genresbyartist as e
			on c.artist = e.artistname
;

create or replace view minio.consulta.artista_por_gravadora as
	select
		a.gravadora
		,count(b.artist) as "artistas que passaram"
	from
		minio.refinado.musicas as a
	inner join
		minio.refinado.artistbytrackid as b
			on a.trackdataid = b.trackid
	group by
		a.gravadora
;

create or replace view minio.consulta.artista_mais_famoso_gravadora as
	select
		a.gravadora
		,a.artist
		,a.followers
	from(
			select
				a.gravadora
				,b.artist
				,cast(round(cast(replace(c.followers, '.', '') as double)) as int) as followers
				,row_number() over (partition by a.gravadora order by c.followers desc) as rn
			from
				minio.refinado.musicas as a
			inner join
				minio.refinado.artistbytrackid as b
					on a.trackdataid = b.trackid
			inner join 
				minio.refinado.artistsdata as c
					on b.artist = c.name
		) as a
	where
		a.rn = 1
	order by
		a.followers desc
;
    