<template>
  <ul class="sidebar-menu">
    <li class="header">代码检查</li>
    <li class="pageLink" v-on:click="toggleMenu">
      <router-link to="/jobs"><i class="fa fa-car"></i>
        <span class="page">Job</span>
        <small class="label pull-right bg-green">Pylint</small>
      </router-link>
    </li>
      
    <li class="header">规范</li>
    <li class="pageLink" v-on:click="toggleMenu">
      <router-link to="/guides">
        <i class="fa fa-book"></i>
        <span class="page">python code style</span>
      </router-link>
    </li>
    <li class="pageLink" v-on:click="toggleMenu">
      <router-link to="/examples">
        <i class="fa fa-bug"></i>
        <span class="page">example</span>
      </router-link>
    </li>
  </ul>
</template>
<script>
export default {
  name: 'SidebarName',
  methods: {
    toggleMenu (event) {
      // remove active from li
      var active = document.querySelector('li.pageLink.active')

      if (active) {
        active.classList.remove('active')
      }
      // window.$('li.pageLink.active').removeClass('active')
      // Add it to the item that was clicked
      event.toElement.parentElement.className = 'pageLink active'
    }
  }
}
</script>
<style>
  /* override default */
  .sidebar-menu>li>a {
    padding: 12px 15px 12px 15px;
  }

  .sidebar-menu li.active>a>.fa-angle-left, .sidebar-menu li.active>a>.pull-right-container>.fa-angle-left {
    animation-name: rotate;
    animation-duration: .2s;
    animation-fill-mode: forwards;
  }

  @keyframes rotate {
    0% {
      transform: rotate(0deg);
    }

    100% {
      transform: rotate(-90deg);
    }
  }
</style>
