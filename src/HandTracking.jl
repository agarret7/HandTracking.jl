module HandTracking

using JSON

""" Listens to HTTP messages containing observations and adds
them to the global list of observations. """
function inference_server(; url::String = "127.0.0.1", port::Integer = 8081)
    HTTP.serve(url, port) do req::HTTP.Request
        data = JSON.parse(String(req.body))
        @show data

        HTTP.Response(200)
    end
end

# inference_server()

include("app.jl")

end # module
