<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Cpv extends Model
{
    protected $connection = 'etl';
    protected $table = 'dim_cpv';
    protected $primaryKey = 'chave_cpv';

    public $timestamps = false;
}
