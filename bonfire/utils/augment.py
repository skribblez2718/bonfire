import os

from typing import Any, List, Optional, Callable, Dict
from abc import abstractmethod

from bonfire.utils.result import BonfireResult


###################################[ start BonfireEvasion ]###################################
class BonfireEvasion:
    """
    Base class for text, audio and visual augmentation.
    This class holds shared functionality across the other augmentation classes.
    """

    #########################[ start __init__ ]#########################
    def __init__(
        self,
        data: List[Dict[str, str]],
        output_file_path: Optional[str] = None,
    ) -> None:
        self.name: str = "BonfireEvasion"
        self.data: List[Dict[str, str]] = data
        self.output_file_path: Optional[str] = output_file_path

        # Ensure output directory exists if output_file_path is provided
        if self.output_file_path:
            output_dir = os.path.dirname(self.output_file_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

    #########################[ end __init__ ]###########################

    #########################[ start get_name ]#########################
    def get_name(self) -> str:
        """
        Returns the name of the augmentation class.

        Returns:
            str: The name of the augmentation class
        """
        return self.name

    #########################[ end get_name ]###########################

    #########################[ start apply ]############################
    @abstractmethod
    def apply(self) -> Any:
        """
        Apply an augmentation method to the given data.

        Returns:
            Any: The augmented data
        """
        pass

    #########################[ end apply ]##############################

    #########################[ start get_available_methods ]############
    @abstractmethod
    def get_available_methods(self) -> List[Callable]:
        """
        Get a list of available augmentation methods.

        Returns:
            List[Callable]: List of available augmentation methods
        """
        pass

    #########################[ end get_available_methods ]##############

    #########################[ start all ]##############################
    @abstractmethod
    def all(self) -> Any:
        """
        Apply all available augmentation methods to the given data.

        Returns:
            Any: The augmented data
        """
        pass

    #########################[ end all ]################################

    #########################[ start generate ]#########################
    def generate(self, logger: "BonfireLogger") -> List[Dict[str, str]]:
        """
        Generate a number of augmented data samples and save to the output file path, grouped by intent.

        Args:
            logger: Active :class:`BonfireLogger`.

        Returns:
            List[Dict[str, str]]: List of generated augmented data
        """
        results = self.apply()
        if self.output_file_path:
            output_dir = os.path.dirname(self.output_file_path)
            filename = os.path.basename(self.output_file_path)
            # Ensure filename includes {intent} for per-intent saving
            if "{intent}" not in filename:
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{{intent}}{ext}"

            BonfireResult.save_by_intent(
                results, output_dir, filename_format=filename, logger=logger
            )
        return results

    #########################[ end generate ]###########################


###################################[ end BonfireEvasion ]#####################################
