<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class DimData extends Model
{
    protected $connection = 'etl';
    protected $table = 'dim_data';
    protected $primaryKey = 'chave_date';
    public $timestamps = false;
}
