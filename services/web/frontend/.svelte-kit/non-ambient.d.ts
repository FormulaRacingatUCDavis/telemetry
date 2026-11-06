
// this file is generated — do not edit it


declare module "svelte/elements" {
	export interface HTMLAttributes<T> {
		'data-sveltekit-keepfocus'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-noscroll'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-preload-code'?:
			| true
			| ''
			| 'eager'
			| 'viewport'
			| 'hover'
			| 'tap'
			| 'off'
			| undefined
			| null;
		'data-sveltekit-preload-data'?: true | '' | 'hover' | 'tap' | 'off' | undefined | null;
		'data-sveltekit-reload'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-replacestate'?: true | '' | 'off' | undefined | null;
	}
}

export {};


declare module "$app/types" {
	export interface AppTypes {
		RouteId(): "/" | "/live" | "/live/camera" | "/live/readings" | "/logs" | "/logs/camera" | "/logs/readings" | "/send";
		RouteParams(): {
			
		};
		LayoutParams(): {
			"/": Record<string, never>;
			"/live": Record<string, never>;
			"/live/camera": Record<string, never>;
			"/live/readings": Record<string, never>;
			"/logs": Record<string, never>;
			"/logs/camera": Record<string, never>;
			"/logs/readings": Record<string, never>;
			"/send": Record<string, never>
		};
		Pathname(): "/" | "/live/camera" | "/live/readings" | "/logs/camera" | "/logs/readings" | "/send";
		ResolvedPathname(): `${"" | `/${string}`}${ReturnType<AppTypes['Pathname']>}`;
		Asset(): "/car.jpg" | "/logo.svg" | "/photo_error.jpg" | "/telemetry_system.jpg" | string & {};
	}
}