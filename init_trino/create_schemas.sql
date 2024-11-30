create schema if not exists minio.bruto with (location = 's3a://bruto/');
create schema if not exists minio.refinado with (location = 's3a://refinado/');


create table if not exists minio.landing.climate_data (
	name VARCHAR,
	datetime VARCHAR,
	tempmax VARCHAR,
	tempmin VARCHAR,
	temp VARCHAR,
	feelslikemax VARCHAR,
	feelslikemin VARCHAR,
	feelslike VARCHAR,
	dew VARCHAR,
	humidity VARCHAR,
	precip VARCHAR,
	precipprob VARCHAR,
	precipcover VARCHAR,
	preciptype VARCHAR,
	snow VARCHAR,
	snowdepth VARCHAR,
	windgust VARCHAR,
	windspeed VARCHAR,
	winddir VARCHAR,
	sealevelpressure VARCHAR,
	cloudcover VARCHAR,
	visibility VARCHAR,
	solarradiation VARCHAR,
	solarenergy VARCHAR,
	uvindex VARCHAR,
	severerisk VARCHAR,
	sunrise VARCHAR,
	sunset VARCHAR,
	moonphase VARCHAR,
	conditions VARCHAR,
	description VARCHAR,
	icon VARCHAR,
	stations VARCHAR
) WITH (
            external_location = 's3a://landing/climate/',
            format = 'CSV',
            skip_header_line_count=1
        );
        
        
-- select * from minio.landing.climate2