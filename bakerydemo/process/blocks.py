from wagtail.blocks import (
    CharBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
)

class EndBlock(StructBlock):
    """
    Custom `StructBlock` that represents the end of a process.
    """

    label = CharBlock()
    description = TextBlock(blank=True, required=False)


class StepBlock(StructBlock):
    """
    Custom `StructBlock` that represents a step.
    """

    label = CharBlock()
    description = TextBlock(blank=True, required=False)


# StreamBlocks
class StepsStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    step_block = StepBlock()
    end_block = EndBlock()
