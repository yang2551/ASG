create table mybase.cubic
(
    `primary` int         not null
        primary key,
    id        int         not null,
    name      varchar(5)  null,
    sg001     varchar(45) not null,
    sg111     varchar(45) not null,
    sg110     varchar(45) not null,
    mask      varchar(25) not null,
    mask001   varchar(10) not null,
    mask111   varchar(10) not null,
    mask110   varchar(10) not null,
    constraint cubic_primary_uindex
        unique (`primary`)
);
create table mybase.hexagonal
(
    `primary` int         not null
        primary key,
    id        int         not null,
    name      varchar(5)  null,
    sg001     varchar(45) not null,
    sg100     varchar(45) not null,
    sg210     varchar(45) not null,
    mask      varchar(25) not null,
    mask001   varchar(10) not null,
    mask100   varchar(10) not null,
    mask210   varchar(10) not null,
    constraint hexagonal_primary_uindex
        unique (`primary`)
);
create table mybase.monoclinic
(
    `primary` int         not null
        primary key,
    id        int         not null,
    name      varchar(5)  null,
    sg001     varchar(45) not null,
    sg100     varchar(45) not null,
    sg010     varchar(45) not null,
    mask      varchar(25) not null,
    mask001   varchar(10) not null,
    mask100   varchar(10) not null,
    mask010   varchar(10) not null,
    constraint monoclinic_primary_uindex
        unique (`primary`)
);
create table mybase.orthorhombic
(
    `primary` int         not null
        primary key,
    id        int         not null,
    name      varchar(5)  null,
    sg001     varchar(45) not null,
    sg100     varchar(45) not null,
    sg010     varchar(45) not null,
    mask      varchar(25) not null,
    mask001   varchar(10) not null,
    mask100   varchar(10) not null,
    mask010   varchar(10) not null,
    constraint orthorhombic_primary_uindex
        unique (`primary`)
);
create table mybase.plane_groups
(
    id           int         not null
        primary key,
    lattice      varchar(10) not null,
    point_groups varchar(10) not null,
    symbol       varchar(45) not null,
    constraint plane_groups_id_uindex
        unique (id),
    constraint plane_groups_symbol_uindex
        unique (symbol)
);
create table mybase.reduced_base
(
    id          int auto_increment
        primary key,
    conditions  varchar(45) null,
    d           varchar(45) not null,
    e           varchar(45) not null,
    f           varchar(45) not null,
    type        varchar(45) not null,
    symmetry    varchar(45) not null,
    trans       varchar(45) not null,
    bravais     varchar(45) not null,
    bravaistype varchar(5)  null,
    constraint ID_UNIQUE
        unique (id)
);
create table mybase.tetragonal
(
    `primary` int         not null
        primary key,
    id        int         not null,
    name      varchar(5)  null,
    sg001     varchar(45) not null,
    sg100     varchar(45) not null,
    sg110     varchar(45) not null,
    mask      varchar(25) not null,
    mask001   varchar(10) not null,
    mask100   varchar(10) not null,
    mask110   varchar(10) not null,
    constraint tetragonal_primary_uindex
        unique (`primary`)
);
create table mybase.triclinic
(
    id    int         not null,
    name  varchar(5)  null,
    sg001 varchar(45) not null,
    sg100 varchar(45) not null,
    sg010 varchar(45) not null,
    mask  varchar(25) not null
);
create table mybase.trigonal
(
    `primary` int         not null
        primary key,
    id        int         not null,
    name      varchar(5)  null,
    sg001     varchar(45) not null,
    sg100     varchar(45) not null,
    sg210     varchar(45) not null,
    mask      varchar(25) not null,
    mask001   varchar(10) not null,
    mask100   varchar(10) not null,
    mask210   varchar(10) not null,
    constraint trigonal_primary_uindex
        unique (`primary`)
);
