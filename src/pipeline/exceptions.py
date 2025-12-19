class PipelineError(Exception):
    """Pipeline module base exception"""
    pass

class ConfigError(PipelineError):
    """Pipeline configuration error"""
    pass

class ProcessorError(PipelineError):
    """Processor error"""
    pass

class FormatterError(PipelineError):
    """Formatter error"""
    pass
