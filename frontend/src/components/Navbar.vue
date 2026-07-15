<script setup>
import { useRouter } from 'vue-router';


const routes = useRouter().getRoutes() .filter(route=>
  route.name && route.name!=="home"
);
function isActive(route) {
  return route.path === useRouter().path
}

const closeOffcanvas =()=> {
  const offcanvasElement = document.getElementById('offcanvasNavbar')
  if (!offcanvasElement) return console.error('offcanvasElement non trovato');

  const offcanvas = $bootstrap.Offcanvas.getInstance(offcanvasElement)
  if (!offcanvas) return console.error('offcanvas non trovato');

  offcanvas.hide()
}
</script>
<template>
  <nav style="padding-top: 3.5rem;">
    <div class="p-0 navbar navbar-expand-sm fixed-top shadow bg-dark z-3" data-bs-theme="dark">
      <div class="p-2 container">

        <!-- BURGER BUTTON FOR OFFCANVAS (MOBILE ONLY) -->
        <button class="navbar-toggler d-md-none"
                type="button"
                data-bs-toggle="offcanvas"
                data-bs-target="#offcanvasNavbar"
                aria-controls="offcanvasNavbar"
                aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- LOGO 
        <RouterLink class="navbar-brand"
                  to="/"
                  active-class="active"
                  :exact="true">
           <i class="bi bi-house"></i>
        </RouterLink>-->

        <!-- OFFCANVAS PER MOBILE -->
        <div class="offcanvas offcanvas-start bg-dark text-white z-4"
            tabindex="-1"
            id="offcanvasNavbar"
            aria-labelledby="offcanvasNavbarLabel">
          <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Menù</h5>
            <button type="button"
                    class="btn-close btn-close-white"
                    data-bs-dismiss="offcanvas"
                    aria-label="Close"></button>
          </div>
          <div class="offcanvas-body">
            <ul class="navbar-nav flex-grow-1">

              <li v-for="route in routes" :key="route.path" class="nav-item">
                  <RouterLink class="nav-link text-white"
                            :to="route.path"
                            :aria-current="isActive(route) ? 'page' : null"
                            @click="closeOffcanvas()">
                            <span :class="{ 'text-info fw-bold': isActive(route) }">
                              {{ route.meta?.title }}
                            </span>
                  </RouterLink>
                </li>

              </ul>
          </div>
        </div>

        <!-- PROFILE LINK -->
        <a href="http://localhost:8000/home/" class="nav-link text-white">
          <i class="bi bi-house"></i>
          <span class="ms-2 d-none d-md-inline">Home</span>
        </a>

      </div>
    </div>
  </nav>
</template>

