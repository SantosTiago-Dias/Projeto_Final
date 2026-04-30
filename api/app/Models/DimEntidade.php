<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class DimEntidade extends Model
{
    protected $connection = 'etl';
    protected $table = 'dim_entidade';
    protected $primaryKey = 'chave_entidade';
    public $timestamps = false;
}
