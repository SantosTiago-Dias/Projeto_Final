<?php

namespace App\Http\Controllers;

use App\Models\Terms;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;

class TermsController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $terms = Cache::rememberForever('terms', fn() => Terms::all()->toArray());

        return response()->json($terms);
    }
}
