import quickjs
import requests
import json

def py_fetch(url: str, options: str = "{}"):
    """Python bridge for JS fetch API."""
    try:
        opts = json.loads(options)
        method = opts.get("method", "GET")
        headers = opts.get("headers", {})
        
        response = requests.request(method, url, headers=headers, timeout=10)
        
        return json.stringify({
            "status": response.status_code,
            "url": response.url,
            "text": response.text
        })
    except Exception as e:
        return json.stringify({"status": 500, "error": str(e), "text": ""})

def run_scraper_script(script_code: str, function_name: str, args: list):
    """
    Executes a JavaScript scraper extension securely in a QuickJS sandbox.
    Includes a polyfilled fetch API bridged to Python's requests module.
    """
    context = quickjs.Context()
    
    # Expose the python fetch function to the JS environment
    context.add_callable("py_fetch", py_fetch)
    
    # Inject JS polyfill that wraps py_fetch to look like the standard Web API
    polyfill = """
    async function fetch(url, options = {}) {
        const resultStr = py_fetch(url, JSON.stringify(options));
        const result = JSON.parse(resultStr);
        return {
            status: result.status,
            url: result.url,
            text: async () => result.text,
            json: async () => JSON.parse(result.text)
        };
    }
    """
    context.eval(polyfill)
    
    # Evaluate the extension script
    context.eval(script_code)
    
    # Build JS function call
    args_str = ", ".join(repr(a) for a in args)
    call_code = f"{function_name}({args_str})"
    
    try:
        result = context.eval(call_code)
        return result
    except quickjs.JSException as e:
        print(f"Extension error: {e}")
        return None

def test_runner():
    mock_extension = """
    function searchManga(query) {
        // Mock Keiyoushi/Mangayomi scraper logic
        if (query === 'berserk') {
            return JSON.stringify([
                {id: 1, title: 'Berserk', url: '/manga/berserk'}
            ]);
        }
        return JSON.stringify([]);
    }
    """
    res = run_scraper_script(mock_extension, "searchManga", ["berserk"])
    print(f"JS Runner result: {res}")
