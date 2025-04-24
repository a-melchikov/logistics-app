import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "@/pages/LoginPage.vue";
import OrdersPage from "@/pages/OrdersPage.vue";
import VehiclesPage from "@/pages/VehiclesPage.vue";
import AdminPanel from "@/pages/AdminPanel.vue";
import VehicleDetailPage from "@/pages/VehicleDetailPage.vue";
import OrderDetailPage from "@/pages/OrderDetailPage.vue";

export const routes = [
  { path: "/", redirect: "/orders" },
  { path: "/login", component: LoginPage },
  { path: "/orders", component: OrdersPage },
  {
    path: "/orders/:id",
    name: "OrderDetail",
    component: OrderDetailPage,
    props: true,
  },
  { path: "/vehicles", component: VehiclesPage },
  {
    path: "/vehicles/:id",
    name: "VehicleDetail",
    component: VehicleDetailPage,
    props: true,
  },
  { path: "/admin", component: AdminPanel },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
