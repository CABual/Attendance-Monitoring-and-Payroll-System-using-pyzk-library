<!DOCTYPE html> 
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">  
<head> 
    <meta charset="UTF-8"> 
    <meta name="viewport"
          content="width=device-width, 
                   initial-scale=1.0"> 
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>{{ config('app.name', 'Laravel') }}</title>

</head> 
  
<body> 
  
    <div class="container-fluid p-0 d-flex h-100"> 
        <div id="bdSidebar" 
             class="d-flex flex-column  
                    flex-shrink-0  
                    p-3 bg-primary 
                    text-white offcanvas-md offcanvas-start"> 
            <a href="#" 
               class="navbar-brand"> 
            </a><hr> 
            <ul class="mynav nav nav-pills flex-column mb-auto"> 
                <li class="nav-item mb-1"> 
                    <a href="#"> 
                        <i class="fa-regular fa-user"></i> 
                        Dashboard 
                    </a> 
                </li> 
  
                <li class="nav-item mb-1"> 
                    <a href="{{ route('properties.index') }}"> 
                        <i class="fa-regular fa-bookmark"></i> 
                        Properties
                        <span class="notification-badge">5</span> 
                    </a> 
                </li> 
                <li class="nav-item mb-1"> 
                    <a href="{{ route('advertisements.index') }}"> 
                        <i class="fa-regular fa-newspaper"></i> 
                        Advertisements 
                    </a> 
                </li> 
                <li class="nav-item mb-1"> 
                    <a href="{{ route('article.index') }}"> 
                        <i class="fa-solid fa-archway"></i> 
                        Articles 
                    </a> 
                </li> 
                <li class="nav-item mb-1"> 
                    <a href="{{ route('quotes.index') }}"> 
                        <i class="fa-solid fa-graduation-cap"></i> 
                        Quotes 
                    </a> 
                </li> 
  
                 
            </ul> 
            <hr> 
            <div class="dropdown pb-4">
                <a href="#" class="d-flex align-items-center text-white text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown" aria-expanded="false">
                    <img src="https://github.com/mdo.png" alt="hugenerd" width="30" height="30" class="rounded-circle">
                    <span class="d-none d-sm-inline mx-1">{{ Auth::user()->name }}</span>
                </a>
                <ul class="dropdown-menu dropdown-menu-dark text-small shadow">
                    <li><a class="dropdown-item" href="#">View Profile</a></li>
                        <hr class="dropdown-divider">
                        
                    <li><a class="dropdown-item" href="{{ route('logout') }}"
                        onclick="event.preventDefault();
                                      document.getElementById('logout-form').submit();">
                         {{ __('Logout') }}
                     </a>

                     <form id="logout-form" action="{{ route('logout') }}" method="POST" class="d-none">
                         @csrf
                     </form></li>
                </ul>
            </div>
            <div class="d-flex"> 
  
                <i class="fa-solid fa-book  me-2"></i> 
                <span> 
                    <h6 class="mt-1 mb-0"> 
                          Geeks for Geeks Learning Portal 
                      </h6> 
                </span> 
            </div> 
        </div> 
  
        <div class="bg-light flex-fill"> 
            <div class="p-2 d-md-none d-flex text-white bg-primary"> 
                <a href="#" class="text-white" 
                   data-bs-toggle="offcanvas"
                   data-bs-target="#bdSidebar"> 
                    <i class="fa-solid fa-bars"></i> 
                </a> 
                <span class="ms-3">GFG Portal</span> 
            </div> 
            <div class="p-4"> 
                <nav style="--bs-breadcrumb-divider:'>';font-size:14px"> 
                    <ol class="breadcrumb"> 
                        <li class="breadcrumb-item"> 
                            <i class="fa-solid fa-house"></i> 
                        </li> 
                        <li class="breadcrumb-item">@yield('page_name')</li> 
                        {{-- <li class="breadcrumb-item">{{ Auth::user()->name }} --}}
                        </li> 
                    </ol> 
                </nav> 
  
                <hr> 
                <div class="row"> 
                    <div class="col-md"> 
                        @yield('content')            
                                
                    </div> 
                </div> 
            </div> 
  
        </div> 
    </div> 
</body> 
  
</html>