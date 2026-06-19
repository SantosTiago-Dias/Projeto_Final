<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Terms extends Model
{
    protected $connection = 'etl';
    protected $table = 'terms';
    protected $primaryKey = 'id';

    public $timestamps = false;
}
