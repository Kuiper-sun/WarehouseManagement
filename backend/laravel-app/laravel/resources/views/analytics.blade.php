<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics Dashboard - Thumbworx</title>
    {{-- Using Tailwind's Play CDN for full feature access --}}
    <script src="https://cdn.tailwindcss.com"></script>
    {{-- We'll use Font Awesome for icons --}}
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    {{-- A little custom CSS to make the gradient header possible --}}
    <style>
        .bg-gradient-header {
            background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        }
    </style>
</head>
<body class="bg-slate-900 text-slate-300 font-sans">

    <div id="app-container" class="flex flex-col min-h-screen">

        {{-- Header Section --}}
        <header class="bg-slate-800 shadow-lg border-b border-slate-700 sticky top-0 z-10">
            <nav class="container mx-auto px-6 py-4">
                <div class="flex items-center justify-between">
                    {{-- App Branding --}}
                    <div class="text-white font-bold text-2xl">
                        <a href="#" class="flex items-center">
                            <i class="fas fa-cubes-stacked mr-3 text-blue-400"></i>
                            <span>Thumbworx</span>
                        </a>
                    </div>
                    {{-- Primary Navigation --}}
                    <div class="hidden md:flex items-center space-x-8">
                        <a href="#" class="text-slate-300 hover:text-blue-400 transition-colors duration-300">Home</a>
                        <a href="#" class="text-slate-300 hover:text-blue-400 transition-colors duration-300">Main Dashboard</a>
                        <a href="/analytics" class="text-white font-semibold border-b-2 border-blue-500 pb-1">Analytics</a>
                    </div>
                    {{-- User Profile Area --}}
                    <div class="hidden md:flex items-center">
                        <span class="text-slate-400 mr-4">Welcome, Admin</span>
                        <img class="h-10 w-10 rounded-full object-cover" src="https://i.pravatar.cc/150" alt="User avatar">
                    </div>
                    {{-- Mobile Menu Button --}}
                    <div class="md:hidden">
                        <button class="text-white focus:outline-none">
                            <i class="fas fa-bars"></i>
                        </button>
                    </div>
                </div>
            </nav>
        </header>

        {{-- Main Content Section --}}
        <main class="container mx-auto px-6 py-8 flex-grow">

            {{-- Page Title and Live Indicator --}}
            <div class="flex items-center justify-between mb-8">
                <h1 class="text-4xl font-bold text-white">Live Analytics Dashboard</h1>
                <div class="flex items-center text-sm bg-green-500/20 text-green-400 px-3 py-1 rounded-full">
                    <i class="fas fa-circle mr-2 text-xs animate-pulse"></i>
                    <span>Live Data Feed</span>
                </div>
            </div>

            {{-- KPI Stat Cards --}}
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <!-- Card 1: Total Alerts -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-red-500/20 p-3 rounded-full">
                            <i class="fas fa-triangle-exclamation text-xl text-red-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">Total Active Alerts</p>
                            <p class="text-3xl font-bold text-white">11</p>
                        </div>
                    </div>
                </div>
                <!-- Card 2: Critical Alerts -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-orange-500/20 p-3 rounded-full">
                            <i class="fas fa-fire-flame-curved text-xl text-orange-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">Critical Alerts</p>
                            <p class="text-3xl font-bold text-white">3</p>
                        </div>
                    </div>
                </div>
                <!-- Card 3: Scans Today -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-blue-500/20 p-3 rounded-full">
                            <i class="fas fa-barcode text-xl text-blue-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">RFID Scans (24h)</p>
                            <p class="text-3xl font-bold text-white">2,481</p>
                        </div>
                    </div>
                </div>
                <!-- Card 4: Products Tracked -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-purple-500/20 p-3 rounded-full">
                            <i class="fas fa-boxes-stacked text-xl text-purple-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">Products Tracked</p>
                            <p class="text-3xl font-bold text-white">8</p>
                        </div>
                    </div>
                </div>
            </div>

            {{-- Iframe Container --}}
            <div class="bg-slate-800 rounded-xl shadow-2xl overflow-hidden border border-slate-700">
                <div class="p-6 border-b border-slate-700">
                    <h2 class="text-xl font-semibold text-white">Metabase Warehouse Overview</h2>
                    <p class="text-sm text-slate-400 mt-1">
                        Use the filters within the dashboard to drill down into specific data points.
                    </p>
                </div>
                
                <div class="p-2 bg-slate-900">
    <iframe
        src="http://localhost:3000/public/dashboard/20b5ff12-91da-486b-ac05-2730a2b7e294"
        frameborder="0"
        width="100%"
        height="800"
        allowtransparency
        class="rounded-lg"
    ></iframe>
</div>
            </div>
        </main>

        {{-- Footer Section --}}
        <footer class="mt-12">
            <div class="text-center py-6 text-slate-500 text-sm border-t border-slate-800">
                &copy; {{ date('Y') }} Thumbworx. All Rights Reserved. Built with Laravel & Docker.
            </div>
        </footer>

    </div>
</body>
</html>